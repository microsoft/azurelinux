# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond stemming %{undefined rhel}

Summary: Utilities to generate, maintain and access the AppStream database
Name:    appstream
Version: 1.1.0
Release: 1%{?dist}

# lib LGPLv2+, tools GPLv2+
License: GPL-2.0-or-later AND LGPL-2.1-or-later
#URL:     http://www.freedesktop.org/wiki/Distributions/AppStream
URL:     https://github.com/ximion/appstream
Source0: https://www.freedesktop.org/software/appstream/releases/AppStream-%{version}.tar.xz

# upstream patches

# upstreamable patches


# needed for cmake auto-provides
BuildRequires: cmake
BuildRequires: meson >= 0.62
BuildRequires: gettext
BuildRequires: git-core
BuildRequires: gperf
BuildRequires: gtk-doc
BuildRequires: intltool
BuildRequires: itstool
%if %{with stemming}
BuildRequires: libstemmer-devel
%endif
BuildRequires: pkgconfig(cairo)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(gdk-pixbuf-2.0)
BuildRequires: pkgconfig(gi-docgen) >= 2021.1
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libfyaml)
BuildRequires: pkgconfig(librsvg-2.0)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(libzstd)
BuildRequires: pkgconfig(pango)
BuildRequires: pkgconfig(Qt6Core) >= 6.2.4
BuildRequires: pkgconfig(xmlb) >= 0.3.14
BuildRequires: pkgconfig(yaml-0.1)
# lrelease
BuildRequires: qt6-linguist
BuildRequires: sed
BuildRequires: vala
BuildRequires: xmlto

Requires: (appstream-data if PackageKit)

%description
AppStream makes it easy to access application information from the
AppStream database over a nice GObject-based interface.

%package devel
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
# -vala subpackage removed in F30
Obsoletes: appstream-vala < 0.12.4-3
Provides: appstream-vala = %{version}-%{release}
%description devel
%{summary}.

%package compose
Summary: Library for generating AppStream data
Requires: %{name}%{?_isa} = %{version}-%{release}
%description compose
%{summary}.

%package compose-devel
Summary:  Development files for %{name}-compose library
Requires: %{name}-compose%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description compose-devel
%{summary}.

%package qt
Summary: Qt6 bindings for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description qt
%{summary}.

%package qt-devel
Summary:  Development files for %{name}-qt bindings
Requires: %{name}-qt%{?_isa} = %{version}-%{release}
Requires: pkgconfig(Qt6Core) >= 6.2.4
%description qt-devel
%{summary}.


%prep
%autosetup -n AppStream-%{version} -S git_am


%build
%{meson} \
 -Dcompose=true \
 -Dqt=true \
 -Dstemming=%{?with_stemming:true}%{!?with_stemming:false} \
 -Dvapi=true

%{meson_build}


%install
%{meson_install}

mkdir -p %{buildroot}/var/cache/swcatalog/{icons,gv,xml}
touch %{buildroot}/var/cache/swcatalog/cache.watch

%find_lang appstream

%if "%{?_metainfodir}" != "%{_datadir}/metainfo"
# move metainfo to right/legacy location
mkdir -p %{buildroot}%{_kf5_metainfodir}
mv %{buildroot}%{_datadir}/metainfo/*.xml \
   %{buildroot}%{_metainfodir}
%endif


%check
%{meson_test} ||:


%posttrans
%{_bindir}/appstreamcli refresh --force >& /dev/null ||:

%transfiletriggerin -- %{_datadir}/swcatalog/xml
%{_bindir}/appstreamcli refresh --force >& /dev/null ||:

%transfiletriggerpostun -- %{_datadir}/swcatalog/xml
%{_bindir}/appstreamcli refresh --force >& /dev/null ||:

%files -f appstream.lang
%doc AUTHORS
%license COPYING
%{_bindir}/appstreamcli
%{_mandir}/man1/appstreamcli.1*
%{_datadir}/appstream/
%dir %{_libdir}/girepository-1.0/
%{_libdir}/girepository-1.0/AppStream-1.0.typelib
%{_libdir}/libappstream.so.5
%{_libdir}/libappstream.so.%{version}
%{_metainfodir}/org.freedesktop.appstream.cli.*.xml
# put in -devel? -- rex
%{_datadir}/gettext/its/metainfo.*
%ghost /var/cache/swcatalog/cache.watch
%dir /var/cache/swcatalog/
%dir /var/cache/swcatalog/icons/
%dir /var/cache/swcatalog/gv/
%dir /var/cache/swcatalog/xml/

%files devel
%{_includedir}/appstream/
%{_libdir}/libappstream.so
%{_libdir}/pkgconfig/appstream.pc
%dir %{_datadir}/gir-1.0/
%{_datadir}/gir-1.0/AppStream-1.0.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/appstream.deps
%{_datadir}/vala/vapi/appstream.vapi
%{_docdir}/appstream/html/
## symlink pointing to ^^, but need to take care, since rpm has
## trouble replacing dirs with symlinks, omit it for now -- rex
%exclude %{_datadir}/gtk-doc/html/appstream
# Maybe this should be split out? -- ngompa
%{_datadir}/installed-tests/appstream/metainfo-validate.test

%files compose
%{_libexecdir}/appstreamcli-compose
%{_mandir}/man1/appstreamcli-compose.1*
%{_libdir}/libappstream-compose.so.0
%{_libdir}/libappstream-compose.so.%{version}
%{_libdir}/girepository-1.0/AppStreamCompose-1.0.typelib
%{_metainfodir}/org.freedesktop.appstream.compose.metainfo.xml

%files compose-devel
%{_includedir}/appstream-compose/
%{_libdir}/libappstream-compose.so
%{_libdir}/pkgconfig/appstream-compose.pc
%{_datadir}/gir-1.0/AppStreamCompose-1.0.gir
%dir %{_datadir}/gtk-doc/
%dir %{_datadir}/gtk-doc/html/
%{_datadir}/gtk-doc/html/appstream-compose

%files qt
%{_libdir}/libAppStreamQt.so.3
%{_libdir}/libAppStreamQt.so.%{version}

%files qt-devel
%{_includedir}/AppStreamQt/
%{_libdir}/cmake/AppStreamQt/
%{_libdir}/libAppStreamQt.so


%changelog
* Fri Sep 26 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Mon Aug 18 2025 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.0.6-1
- rebuilt

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Mar 14 2025 Shawn W. Dunn <sfalken@cloverleaf-linux.org> - 1.0.4-2
- Change appstream-data to a conditional Requires:

* Sun Jan 19 2025 Pavel Solovev <daron439@gmail.com> - 1.0.4-1
- Update to 1.0.4

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 05 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.0.2-3
- Disable stemming support on RHEL

* Sat Mar 09 2024 Alessandro Astone <ales.astone@gmail.com> - 1.0.2-2
- Backport patch to fix installing swcatalog

* Sun Feb 25 2024 Neal Gompa <ngompa@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2
- Clean up some pre-1.0 scriptlet cruft

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Steve Cossette <farchord@gmail.com> - 1.0.1-1
- Update to 1.0.1

* Fri Nov 17 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0 final

* Thu Nov 02 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.0.0~git20231102.d88ed03-1
- Rebase to 1.0.0 git snapshot

* Mon Aug 21 2023 Parag Nemade <pnemade AT fedoraproject DOT org> - 0.16.1-4
- Migrate to SPDX license expression

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.16.1-2
- Disable Qt5 in RHEL 10 builds
- Remove obsolete BuildRequires

* Sat Feb 11 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.16.1-1
- Update to 0.16.1

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 6 2022 Amit Shah <amitshah@fedoraproject.org> - 0.15.5-2
- Make qt deps and builds conditional

* Fri Sep 02 2022 Rex Dieter <rdieter@gmail.com> - 0.15.5-1
- 0.15.5

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 07 2022 Rex Dieter <rdieter@fedoraproject.org> - 0.15.4-1
- 0.15.4

* Tue Apr 19 2022 Rex Dieter <rdieter@fedoraproject.org> 0.15.3-1
- 0.15.3

* Wed Feb 23 2022 Rex Dieter <rdieter@fedoraproject.org> - 0.15.2-1
- 0.15.2
- support only filetriggers

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 29 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.15.1-1
- 0.15.1 (#2028696)
- update triggers to consistently use --force flag on 'appstreamcli refresh' calls

* Tue Oct 12 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.14.6-1
- 0.14.6

* Sat Aug 28 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.14.5-1
- Update to 0.14.5

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 29 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.14.4-1
- 0.14.4

* Sat Apr 03 2021 Neal Gompa <ngompa13@gmail.com> - 0.14.3-2
- Build appstream-compose library for appstream-generator >= 0.8.4

* Mon Mar 08 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.14.3-1
- 0.14.3

* Tue Mar 02 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.14.2-1
- 0.14.2

* Wed Feb 17 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.14.1-1
- 0.14.1

* Thu Feb 04 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.14.0-1
- 0.14.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 07 2020 Rex Dieter <rdieter@fedoraproject.org> - 0.13.1-1
- 0.13.1

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 14 2020 Rex Dieter <rdieter@fedoraproject.org> - 0.12.11-1
- 0.12.11

* Thu Mar 19 2020 Rex Dieter <rdieter@fedoraproject.org> - 0.12.10-1
- 0.12.10

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 10 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.12.9-1
- 0.12.9
- drop dep on publican (#1773385)

* Sat Aug 17 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.12.8-1
- 0.12.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.12.7-1
- 0.12.7
- BR: lmdb

* Sun Mar 03 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.12.6-1
- 0.12.6

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 0.12.4-4
- Move appstream-vala obsoletes to -devel subpackage

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 0.12.4-3
- Use standard vala packaging pattern where vapi files are in -devel

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.12.4-1
- 0.12.4
- pull in some upstream fixes (#1667060)

* Tue Nov 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.12.3-1
- 0.12.3

* Fri Oct 12 2018 Kalev Lember <klember@redhat.com> - 0.12.2-2
- Backport an upstream fix for empty content_rating tags

* Tue Aug 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.12.2-1
- appstream-0.12.2 (#1589595)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 10 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.12.1-1
- appstream-0.12.1 (#1589595)
- use %%ldconfig_scriptlets

* Sun Apr 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.12.0-1
- 0.12.0 (#1563876)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Jan Grulich <jgrulich@redhat.com> - 0.11.8-2
- Fix broken cmake for Qt library

* Fri Jan 26 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.11.8-1
- 0.11.8

* Fri Dec 29 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.11.7-2
- use metainfo dir for f28+

* Fri Nov 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.11.7-1
- 0.11.7

* Mon Oct 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.11.6-1
- 0.11.6

* Thu Sep 14 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.11.5-4
- pull in upstream vala workaround

* Thu Sep 14 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.11.5-3
- hack around broken vala bindings

* Tue Sep 12 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.11.5-2
- use file triggers for cache regen

* Mon Sep 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.11.5-1
- 0.11.5 (#1486970)

* Thu Sep 07 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.11.4-1
- 0.11.4 (#1486970)

* Sun Aug 06 2017 Björn Esser <besser82@fedoraproject.org> - 0.11.2-4
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.11.2-1
- 0.11.2

* Mon Jul 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.11.1-1
- 0.11.1

* Fri May 05 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.11.0-1
- 0.11.0

* Wed Apr 05 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.10.6-1
- 0.10.6

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.10.5-1
- 0.10.5

* Thu Dec 15 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.10.4-1
- 0.10.4

* Tue Nov 15 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.10.3-4
- use /usr/share/appdata, improve /var/cache/app-info

* Mon Nov 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.10.3-2
- pull in upstream crash fix

* Tue Nov 01 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.10.3-1
- 0.10.3
- update scriptlets to use 'refresh' instead of 'refresh-index'

* Fri Sep 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.10.1-3
- s|share/appstream|share/appdata/

* Sat Sep 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.10.1-2
- improve description, drop no-longer-used deps

* Sat Sep 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.10.1-1
- 0.10.1

* Thu Aug 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.9.8-3
- pull in upstream fixes

* Wed Aug 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.9.8-2
- (re)enable vala support (#1367892)

* Fri Aug 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.9.8-1
- 0.9.8

* Thu May 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.9.6-1
- 0.9.6

* Fri Apr 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.9.3-1
- 0.9.3

* Wed Feb 24 2016 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-1
- 0.9.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Dec 13 2015 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-1
- 0.9.0

* Sun Dec 13 2015 Rex Dieter <rdieter@fedoraproject.org> 0.8.6-1
- 0.8.6

* Tue Sep 29 2015 Rex Dieter <rdieter@fedoraproject.org> 0.8.4-3
- Don't abort hitting unknown appstream tags (#1267312)

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> 0.8.4-2
- polish scriptlets
- use --force in %%post
- use %%triggerun -- appstream-data (only on upgrades)
- ignore errors, redirect output to /dev/null

* Tue Sep 08 2015 Rex Dieter <rdieter@fedoraproject.org> 0.8.4-1
- 0.8.4, refresh-index whenever appstream-data is updated too

* Thu Sep 03 2015 Rex Dieter <rdieter@fedoraproject.org> 0.8.3-2
- -devel: fix doc handling, omit gtk-doc symlink (for now)

* Thu Sep 03 2015 Rex Dieter <rdieter@fedoraproject.org> 0.8.3-1
- 0.8.3

* Sat Jun 27 2015 Rex Dieter <rdieter@fedoraproject.org> 0.8.2-1
- 0.8.2

* Sat Jun 27 2015 Rex Dieter <rdieter@fedoraproject.org> 0.8.1-1
- 0.8.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.8.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Wed Jan 28 2015 Rex Dieter <rdieter@fedoraproject.org> 0.8.0-1
- 0.8.0

* Wed Jan 21 2015 Rex Dieter <rdieter@fedoraproject.org> 0.7.6-1
- 0.7.6

* Wed Jan 21 2015 Rex Dieter <rdieter@fedoraproject.org> 0.7.5-2
- -qt: Qt5 support (drop deprecated Qt4-based bindings)

* Tue Jan 13 2015 Rex Dieter <rdieter@fedoraproject.org> 0.7.5-1
- 0.7.5

* Mon Oct 13 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.7.3-1
- 0.7.3
- omit vala support (for now, build broken)

* Tue Sep 30 2014 Rex Dieter <rdieter@fedoraproject.org> 0.7.2-2
- pull in some upstream fixes, fix %%posttrans scriptlet

* Tue Sep 30 2014 Rex Dieter <rdieter@fedoraproject.org> 0.7.2-1
- 0.7.2, ready qt5 support (not enabled yet)

* Fri Sep 12 2014 Rex Dieter <rdieter@fedoraproject.org> 0.7.1-1
- 0.7.1

* Wed Aug 20 2014 Rex Dieter <rdieter@fedoraproject.org> 0.7.0-4
- enable Qt bindings support

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.7.0-2
- Rebuilt for gobject-introspection 1.41.4

* Wed Jul 16 2014 Rex Dieter <rdieter@fedoraproject.org> 0.7.0-1
- 0.7.0

* Sat Jun 28 2014 Rex Dieter <rdieter@fedoraproject.org> 0.6.2-6
- Requires: appstream-data

* Sat Jun 28 2014 Rex Dieter <rdieter@fedoraproject.org> 0.6.2-5
- backport upstream commit to fix appstream-index hang (#1098306)

* Fri Jun 20 2014 Rex Dieter <rdieter@fedoraproject.org> 0.6.2-4
- appstream-index scriptlet hanging, skip for now (#1098306)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Rex Dieter <rdieter@fedoraproject.org> 0.6.2-2
- update URL

* Mon May 12 2014 Rex Dieter <rdieter@fedoraproject.org> 0.6.2-1
- 0.6.2

* Sat Apr 26 2014 Rex Dieter <rdieter@fedoraproject.org> 0.6.1-1
- Appstream-0.6.1, -vala support lives!

* Sat Apr 19 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.6-1
- Appstream-0.6
- Obsoletes: appstream-vala (no longer provided)

* Sun Feb 23 2014 Rex Dieter <rdieter@fedoraproject.org> 0.5-1
- Appstream-0.5

* Fri Jan 31 2014 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-3
- rebuild (PackageKit)

* Mon Nov 04 2013 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-2
- -vala subpkg
- own %%{_libdir}/girepository-1.0, %%{_libdir}/packagekit-plugins (until someone better comes along)

* Sun Nov 03 2013 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-1
- AppStream-0.4.0


